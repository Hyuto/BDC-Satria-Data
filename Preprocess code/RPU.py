# Imports
import os, random, sys
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tqdm import tqdm
from PIL import Image
from sklearn.model_selection import train_test_split
from skimage.transform import rotate

# SEED ALL
SEED = 42
os.environ['PYTHONHASHSEED'] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

class Config(object):
    """
    Config for running in shell
    """
    def __init__(self):
        self.SIZE = 256
        self.TEST_SIZE = 0.15
        self.UP_SAMPLES = [0.5, 1, 2]
        self.UP_SAMPLE_CLASS = None

    def refresh_type_data(self):
        self.SIZE = int(self.SIZE)
        self.TEST_SIZE = float(self.TEST_SIZE)
        if len(self.UP_SAMPLES) > 1:
            self.UP_SAMPLES = [float(x) for x in self.UP_SAMPLES]
        else:
            self.UP_SAMPLES = float(self.UP_SAMPLES)
        self.UP_SAMPLE_CLASS = int(self.UP_SAMPLE_CLASS)

config = Config()

def load_and_preprocess_image(path: str, size = (256, 256)) -> np.ndarray:
    """
    Load & Preprocess Text

    Args:
        path (str): Image Path
        size (tuple, optional): Image resizing plan [Auto 256 x 256]. Defaults to (256, 256).

    Returns:
        np.ndarray: Numpy array dari data gambar yang telah di preprocess
    """
    # Load image to array and then to tensor
    image = img_to_array(load_img(path))
    img = tf.convert_to_tensor(image, dtype=tf.float32)

    # Resampling image to it's center by square
    shapes = tf.shape(img)
    h, w = shapes[-3], shapes[-2]
    dim = tf.minimum(h, w)
    img = tf.image.resize_with_crop_or_pad(img, dim, dim)

    # Resize
    img = tf.image.resize(img, size)

    # Normalize
    img = tf.cast(img, tf.float32) / 255.0

    return img.numpy() # to Numpy

def data_augmentation(x) -> np.ndarray:
    """
    Image Augmentation. Random rotation in range -70 to 70 degree.

    Args:
        x ([np.ndarray]): Array of image

    Returns:
        np.ndarray: Numpy array dari gambar yang telah di augmentasi
    """
    return rotate(x, random.randint(-70, 70), mode='reflect')

def ApplyAUG(TRAIN_X, TRAIN_y, PATH:str, LP, data_aug, up_sample_ratio = 0.2,
             up_sample_class = None, DIR = 'Prep Data + AUG', SIZE = (256, 256)):
    """
    Fungsi untuk mengaplikasikan Preprocess dan Augmentation ke dalam data gambar untuk disimpan
    kedalam direktori/file yang baru.

    Args:
        TRAIN_X ([type]): List atau Array direktori dari gambar
        TRAIN_y ([type]): List atau Array kelas(label) dari TRAIN_X [One Hot Encoding]
        PATH (str): Direktori data gambar
        LP ([type]): Load & Preprocess image function
        data_aug ([type]): Augmentation function
        up_sample_ratio (float, optional): Rasio up sampling yang dikehendaki.. Defaults to 0.2.
        up_sample_class ([type], optional): Spesifikasi kelas yang akan dilakukan Augmentasi. 
                                            Jika ini di isi maka upsample hanya akan dilakukan pada 
                                            kelas yang di spesifikasikan. Defaults to None.
        DIR (str, optional): Direktori tujuan. Defaults to 'Prep Data + AUG'.
        SIZE (tuple, optional): Ukuran gambar. Defaults to (256, 256).
    
    Returns:
        [np.ndarray], [np.ndarray]: Numpy array dari lokasi/direktori gambar yang telah di augmentasi dan
                                    Numpy array dari label gambar.
    """

    def __up_sampling(up_sample_ratio:float, N:int) -> np.ndarray:
        """
        Up Sampling Plan. Randomly select image data according to up_sample_ratio.

        Args:
            up_sample_ratio (float): Up-sampling rasio
            N (int): Populasi

        Returns:
            np.ndarray: [description]
        """
        # Get Div and Mod
        if up_sample_ratio >= 1:
            div, mod = divmod(up_sample_ratio, 1)
        else:
            div, mod = 0, up_sample_ratio
        
        # Sample n file from populations
        n_sample = random.sample(range(N), int(N * mod))
        # Add to main array
        n_AUG = np.array([div] * N) + np.array([1 if i in n_sample else 0 for i in range(N)])

        return np.asarray(n_AUG, dtype = 'int32')

    if up_sample_class != None:
        print(f'[INFO] Up Sampling Kelas {up_sample_class} Sebesar {up_sample_ratio * 100}%')
    else:
        print(f'[INFO] Up Sampling Setiap Kelas Sebesar {up_sample_ratio * 100}%')
    
    TRAIN_X, TRAIN_y = np.asarray(TRAIN_X), np.asarray(TRAIN_y)  # Make sure TRAIN_X & TRAIN_Y is np.array
    os.makedirs(DIR)  # Make Parent Directory
    X, Y = [], []     # Initialize X and Y
    for i in np.unique(TRAIN_y):                    # Loop for every class
        print(f'[INFO] Memproses Kelas {i}..')
        CHILD_DIR = os.path.join(DIR, f'{i}')       # Child/Class Directory
        os.makedirs(CHILD_DIR)
        data = TRAIN_X[TRAIN_y == i]                # Selecting Data based on Class

        if up_sample_class != None:                 # Up Sampling Plan
            if i == up_sample_class:
                n_AUG = __up_sampling(up_sample_ratio, len(data))
            else:
                n_AUG = [0] * len(data)
        else:
            n_AUG = __up_sampling(up_sample_ratio, len(data))

        for k, file in enumerate(tqdm(data)):       # Loop Through
            IMAGE_DIR = os.path.join(CHILD_DIR, f'{file[:-4]}.png') # Image save path
            img = LP(PATH + file, size=SIZE)   # Load and Preprocess Image
            tf.keras.preprocessing.image.save_img(IMAGE_DIR, img)   # TF save image
            X.append(IMAGE_DIR); Y.append(i)    # Record path and label to X and Y

            for j in range(n_AUG[k]):   # Loop Through Augmentation Up Sample plan
                AUG_DIR = os.path.join(CHILD_DIR, f'AUG {j + 1}_{file[:-4]}.png') # AUG save path
                aug = data_aug(img)     # Augmented Image
                tf.keras.preprocessing.image.save_img(AUG_DIR, aug) # TF save augmented image
                X.append(AUG_DIR); Y.append(i) # Record path and label to X and Y
        print(f'[INFO] Selesai Memproses Kelas {i}')
        print('[INFO] ' + f'Banyak Data Kelas {i} setelah proses sebanyak {len(os.listdir(CHILD_DIR))} gambar'.title())
    print(f'[INFO] Saved to {DIR}')
    return X, Y

def name_based_config(config, arg):
    """
    Name based
    """
    if ':' in arg:
        tipe, value = arg.split(':')
        if '-' in value:
            value = [float(x) for x in value.split('-')]
            exec(f'config.{tipe} = {value}')
        else: exec(f'config.{tipe} = float({value})')
    else: pass

def get_config(config, args):
    """
    Get config from CMD
    """
    try: config.SIZE = int(args[2])
    except: 
        try: name_based_config(config, args[2])
        except: pass
    try: config.TEST_SIZE = float(args[3])
    except: 
        try: name_based_config(config, args[3])
        except: pass
    try: config.UP_SAMPLES = [float(x) for x in args[4].split('-')]
    except: 
        try: name_based_config(config, args[4])
        except: pass
    try: config.UP_SAMPLE_CLASS = args[5]
    except: 
        try: name_based_config(config, args[5])
        except: pass 
    config.refresh_type_data()

if __name__ == "__main__":
    # System ARGS
    args = sys.argv
    TRAIN_PATH = args[1]
    get_config(config, args)

    print('[INFO] Starting Program to Preprocess & Upsampling Data Gambar..')
    print('[INFO] Config :')
    print(f'       Image Path        : {TRAIN_PATH}')
    print(f'       Image Resize Plan : {config.SIZE}')
    print(f'       Split Valid Size  : {config.TEST_SIZE * 100}%')
    print(f"       Rasio Upsample    : {' , '.join([str(x) for x in config.UP_SAMPLES])}")
    print(f"       Upsample Class    : {config.UP_SAMPLE_CLASS if config.UP_SAMPLE_CLASS != None else 'ALL'}")
    print()

    # X and Y
    data = pd.read_csv('https://raw.githubusercontent.com/Hyuto/BDC-Satria-Data/master/TRAIN.CSV')
    TRAIN_X, VAL_X, TRAIN_y, VAL_y = train_test_split(data.X.values, data.y.values, test_size = config.TEST_SIZE, 
                                                       random_state = SEED, stratify = data.y.values)

    # Up Sample Train Data
    print('[INFO] Memulai Preprocess dan Augmentasi Pada Data Latih')
    for i, up_sample in enumerate(config.UP_SAMPLES):
        print(f'[INFO] Tahap {i + 1}')
        DIREC = f'Up-Sample-0-by-{int(up_sample * 100)}%'
        TEMP_X, TEMP_Y = ApplyAUG(TRAIN_X, TRAIN_y, TRAIN_PATH, up_sample_ratio = up_sample, 
                                  DIR = DIREC, up_sample_class = config.UP_SAMPLE_CLASS, data_aug = data_augmentation,
                                  SIZE = (config.SIZE, config.SIZE), LP = load_and_preprocess_image)
        df = pd.DataFrame({'DIR' : TEMP_X, 'label' : TEMP_Y})
        df.to_csv(DIREC + '/Keterangan.csv', index = False)
        print()

    # Valid Data
    print('[INFO] Memulai Preprocess pada Data Validitas')
    DIREC = 'Validitas'
    TEMP_X, TEMP_Y = ApplyAUG(VAL_X, VAL_y, TRAIN_PATH, up_sample_ratio = 0, 
            DIR = DIREC, data_aug = data_augmentation, 
            SIZE = (config.SIZE, config.SIZE), LP = load_and_preprocess_image)
    df = pd.DataFrame({'DIR' : TEMP_X, 'label' : TEMP_Y})
    df.to_csv(DIREC + '/Keterangan.csv', index = False)
    print()

    print('[INFO] Selesai')
    print('© Catatan Cakrawala 2020')
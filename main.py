import time
from pathlib import Path
import pyautogui

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
retryDelay = 0.01


def resolve_image_path(path):
    p = Path(path)
    if p.is_absolute():
        return str(p)
    return str(IMAGES_DIR / p)

def image_file(name):
    return resolve_image_path(name)


def find_image(image_path):
    '''Gives XY coordinates of image'''
    try:
        return pyautogui.locateCenterOnScreen(resolve_image_path(image_path), confidence=0.78)
    except Exception:
        return None


def click_image(image_path, timeout=0.4):
    end = time.time() + timeout
    while time.time() < end:
        pos = find_image(image_path)
        if pos:
            pyautogui.click(pos)
            return True
        time.sleep(retryDelay)
    return False

def click_all(image_path, timeout=0.4):
    end = time.time() + timeout
    while time.time() < end:
        matches = list(pyautogui.locateAllOnScreen(resolve_image_path(image_path), confidence=0.5))
        if matches:
            for box in matches:
                pyautogui.click(pyautogui.center(box))
            return True
        time.sleep(retryDelay)
    return False


def click_any(images, timeout=0.4):
    end = time.time() + timeout
    while time.time() < end:
        for image_path in images:
            pos = find_image(image_path)
            if pos:
                pyautogui.click(pos)
                return True
        time.sleep(retryDelay)
    return False


def click_required(image_name, timeout=0.4, max_tries=2):
    for attempt in range(1, max_tries + 1):
        if click_image(image_file(image_name), timeout=0.4):
            return True
        
        print(f"{image_name} not found, try {attempt}/{max_tries}")
        if attempt < max_tries:
            time.sleep(retryDelay)
    return False


def click_required_any(image_names, label, timeout=5, max_tries=3):
    images = [image_file(name) for name in image_names]
    for attempt in range(1, max_tries + 1):
        if click_any(images, timeout=timeout):
            return True
        print(f"{label} not found, try {attempt}/{max_tries}")
        if attempt < max_tries:
            time.sleep(retryDelay)
    return False


def drag_and_drop(start_image, end_image, timeout=0.4, max_tries=3):
    end = time.time() + timeout
    while time.time() < end:
        start = find_image(start_image)
        end_pos = find_image(end_image)
        if start and end_pos:
            pyautogui.moveTo(start.x, start.y)
            pyautogui.mouseDown(button='left')
            pyautogui.moveTo(end_pos.x, end_pos.y, duration=0.01)
            pyautogui.mouseUp(button='left')
            return True
        time.sleep(retryDelay)
        pyautogui.mouseUp(button='left')
    return False

def run():
    '''This is where the magic happens'''
    while True:
        while find_image("coin.png") is not None:
            click_image("coin.png")
            
        while find_image("coin_gold.png") is not None:
            click_image("coin_gold.png")

        while find_image("water_small.png") is not None:
            drag_and_drop("water_big.png", "water_small.png")

        while find_image("spray_small.png") is not None:
            drag_and_drop("spray_big.png", "spray_small.png")

        while find_image("music_small.png") is not None:
            drag_and_drop("music_big.png", "music_small.png")

        while find_image("fertilizer_small.png") is not None:
            drag_and_drop("fertilizer_big.png", "fertilizer_small.png")
        time.sleep(retryDelay)
        

if __name__ == "__main__":
    run()

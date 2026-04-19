import time
from pathlib import Path
import pyautogui

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
retryDelay = 0.001
timeout = 0.12
confidence = 0.85  # How confident are we feeling (%)?


def resolve_image_path(path):
    p = Path(path)
    if p.is_absolute():
        return str(p)
    return str(IMAGES_DIR / p)


def image_file(name):
    return resolve_image_path(name)


def click():
    pyautogui.mouseDown(button="left")
    pyautogui.mouseUp(button="left")


def find_image(image_path):
    """Gives XY coordinates of image"""
    try:
        return pyautogui.locateCenterOnScreen(
            resolve_image_path(image_path), confidence=confidence
        )
    except Exception:
        return None


def click_image(image_path, timeout=timeout):
    end = time.time() + timeout
    while time.time() < end:
        pos = find_image(image_path)
        if pos:
            pyautogui.click(pos)
            return True
        time.sleep(retryDelay)
    return False


def click_all(image_path, timeout=timeout):
    end = time.time() + timeout
    while time.time() < end:
        matches = list(
            pyautogui.locateAllOnScreen(
                resolve_image_path(image_path), confidence=confidence
            )
        )
        if matches:
            for box in matches:
                pyautogui.click(pyautogui.center(box))
            return True
        time.sleep(retryDelay)
    return False


def drag_and_drop(start_image, end_image, timeout=timeout):
    end = time.time() + timeout
    while time.time() < end:
        start = find_image(start_image)
        end_pos = find_image(end_image)
        if start and end_pos:
            pyautogui.moveTo(start.x, start.y)
            click()
            pyautogui.moveTo(end_pos.x, end_pos.y, duration=0.15)
            time.sleep(retryDelay)
            click()
            return True
        click()
    return False


def run():
    """This is where the magic happens 🧙✨"""
    while True:
        if find_image("coin.png") != None:
            click_image("coin.png")

        if find_image("coin_gold.png") != None:
            click_image("coin_gold.png")

        if find_image("water_small.png") != None:
            drag_and_drop("water_big.png", "water_small.png")

        if find_image("spray_small.png") != None:
            drag_and_drop("spray_big.png", "spray_small.png")

        if find_image("music_small.png") != None:
            drag_and_drop("music_big.png", "music_small.png")

        if find_image("fertilizer_small.png") != None:
            drag_and_drop("fertilizer_big.png", "fertilizer_small.png")
        time.sleep(retryDelay)


if __name__ == "__main__":
    # time.sleep(4) # Optional starting delay
    run()

import argparse
import glob
import logging
import os
from datetime import datetime

import openslide
from tqdm import tqdm

APPROX_LEVELS = {"x4": 1, "x16": 2, "x64": 3}


def setup_logger(log_folder: str):
    """
    Sets up the logger with a file handler and a stream handler.

    Args:
        log_folder (str): Path to the folder where the log file will be saved.

    Returns:
        logger (logging.Logger): Configured logger.
    """
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_folder, f"log_svs_{current_datetime}.log")

    logger = logging.getLogger("SVSProcessor")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def read_svs_images(
    source_folder: str,
    logger: logging.Logger,
):
    """
    Reads all SVS images from the source folder recursively.

    Args:
        source_folder (str): The source folder to search for SVS images.
        logger (logging.Logger): The logger for logging messages.

    Returns:
        list: A list of paths to the SVS images.
    """
    slides = glob.glob(os.path.join(source_folder, "**", "*.svs"), recursive=True)
    if not slides:
        logger.warning(f"No SVS images found in {source_folder}")
    return slides


def export_images(
    slides: list,
    approximation: str,
    source_folder: str,
    output_folder: str,
    logger: logging.Logger,
):
    """
    Exports images to PNG format with the specified approximation level and saves slide info.

    Args:
        slides (list): List of paths to the SVS images.
        approximation (str): Approximation level for image export (x4, x16, x64).
        source_folder (str): Path to the source folder containing SVS images.
        output_folder (str): Path to the output folder for exported images.
        logger (logging.Logger): The logger for logging messages.
    """
    os.makedirs(output_folder, exist_ok=True)
    logger.info(f"Exporting images to {output_folder}")

    info_file = os.path.join(output_folder, f"slides_info_{approximation}.txt")

    with open(info_file, "w") as f:
        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(f"Date: {current_datetime}\n\n")

    for slide in tqdm(slides, desc="Processing slides", unit="slide"):
        slide_name = os.path.splitext(os.path.basename(slide))[0]
        relative_path = os.path.relpath(slide, source_folder)
        output_slide_folder = os.path.join(
            output_folder, os.path.dirname(relative_path)
        )
        os.makedirs(output_slide_folder, exist_ok=True)

        try:
            with openslide.OpenSlide(slide) as sld:
                scale_level = APPROX_LEVELS[approximation]
                rgb_slide = sld.read_region(
                    (0, 0), scale_level, sld.level_dimensions[scale_level]
                )
                rgb_slide = rgb_slide.convert("RGB")
                output_path = os.path.join(
                    output_slide_folder, f"{slide_name}_{approximation}.png"
                )
                rgb_slide.save(output_path, format="PNG", quality=100)
                save_slide_info(sld, slide_name, info_file, output_path, logger)
        except openslide.OpenSlideError as ose:
            logger.error(f"OpenSlide error processing slide {slide_name}: {ose}")
        except Exception as e:
            logger.error(f"Unexpected error processing slide {slide_name}: {e}")


def save_slide_info(
    slide: openslide.OpenSlide,
    slide_name: str,
    info_file: str,
    output_path: str,
    logger: logging.Logger,
):
    """
    Saves slide information to the info file.

    Args:
        slide (openslide.OpenSlide): The OpenSlide object representing the slide.
        slide_name (str): The name of the slide.
        info_file (str): Path to the info file.
        logger (logging.Logger): The logger for logging messages.
    """
    try:
        original_file_size = os.path.getsize(slide._filename) / (
            1024 * 1024
        )  # Convert to MB
        saved_file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB

        with open(info_file, "a") as f:
            f.write(f"Slide: {slide_name}\n")
            f.write(f"Dimensions: {slide.level_dimensions}\n")
            f.write(f"Number of Levels: {slide.level_count}\n")
            f.write(f"Downsamples: {slide.level_downsamples}\n")
            f.write(f"Original File Size: {original_file_size:.2f} MB\n")
            f.write(f"Saved File Size: {saved_file_size:.2f} MB\n")
            f.write("\n")
    except Exception as e:
        logger.error(f"Error saving slide info for {slide_name}: {e}")


def main():
    """
    Main function to process SVS images, convert them to PNGs, and save slide information.
    """
    parser = argparse.ArgumentParser(description="Process SVS images.")
    parser.add_argument(
        "-a",
        "--approximation",
        type=str,
        choices=["x4", "x16", "x64"],
        default="x16",
        help="Approximation level for image export",
    )
    parser.add_argument(
        "-s",
        "--source_folder",
        type=str,
        required=True,
        help="Path to the source folder containing SVS images",
    )
    parser.add_argument(
        "-o",
        "--output_folder",
        type=str,
        help="Path to the output folder for exported images",
    )
    parser.add_argument(
        "-l",
        "--log_folder",
        type=str,
        default=os.path.dirname(os.path.realpath(__file__)),
        help="Path to the folder where the log file will be saved (default: current directory)",
    )
    args = parser.parse_args()

    if not args.output_folder:
        source_folder_name = os.path.basename(os.path.normpath(args.source_folder))
        args.output_folder = os.path.join(
            os.path.dirname(args.source_folder),
            f"{source_folder_name}_{args.approximation}_pngs",
        )

    os.makedirs(args.output_folder, exist_ok=True)

    logger = setup_logger(args.log_folder)
    logger.info("Started processing SVS images")

    # Log all arguments at the beginning of the log file
    logger.info(f"Arguments: {vars(args)}")

    slides = read_svs_images(args.source_folder, logger)

    if not slides:
        logger.error(f"No SVS images found in {args.source_folder}")
        return

    logger.info(f"Found {len(slides)} SVS images in {args.source_folder}")

    export_images(
        slides, args.approximation, args.source_folder, args.output_folder, logger
    )

    logger.info("Finished processing SVS images")


if __name__ == "__main__":
    main()

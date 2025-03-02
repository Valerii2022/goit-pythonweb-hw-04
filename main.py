import os
import shutil
import asyncio
import logging
from pathlib import Path
import argparse

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

async def create_subfolder_for_extension(output_folder, extension):
    subfolder_path = output_folder / extension
    if not subfolder_path.exists():
        os.makedirs(subfolder_path)
    return subfolder_path

async def copy_file(file_path, output_folder):
    try:
        extension = file_path.suffix.lstrip('.').lower() 
        if extension:
            subfolder = await create_subfolder_for_extension(output_folder, extension)
            target_path = subfolder / file_path.name
            shutil.copy(file_path, target_path)
            logger.info(f"Файл {file_path.name} скопійовано до {target_path}")
        else:
            logger.warning(f"Файл {file_path.name} не має розширення і не буде оброблений.")
    except Exception as e:
        logger.error(f"Помилка при копіюванні файлу {file_path.name}: {e}")

async def read_folder(source_folder, output_folder):
    try:
        for root, _, files in os.walk(source_folder):
            for file_name in files:
                file_path = Path(root) / file_name
                await copy_file(file_path, output_folder)
    except Exception as e:
        logger.error(f"Помилка при читанні папки {source_folder}: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Сортування файлів за розширенням")
    parser.add_argument("source_folder", type=str, help="Вихідна папка")
    parser.add_argument("output_folder", type=str, help="Цільова папка")
    args = parser.parse_args()

    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.exists() or not source_folder.is_dir():
        logger.error(f"Вихідна папка {source_folder} не існує або не є директорією.")
        return

    if not output_folder.exists():
        os.makedirs(output_folder)

    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())

import os

from s3_client import S3Client
from raster_processor import RasterProcessor


# https://s3.console.aws.amazon.com/s3/buckets/ceres-technical-challenge?region=us-west-2&tab=objects

def main():
    s3_client = S3Client(
        bucket_name="ceres-technical-challenge",
        region_name="us-west-2",
    )

    tiff_files = s3_client.list_tiff_images()

    if not tiff_files:
        print("No TIFF files found in the bucket.")
        return

    directory_path = "files"
    os.makedirs(directory_path, exist_ok=True)

    raster_key = tiff_files[0]
    print(f"Selected S3 file: {raster_key}")

    filename = os.path.basename(raster_key)
    local_raster = f"{directory_path}/{filename}"
    local_png = f"{directory_path}/{os.path.splitext(filename)[0]}.png"

    s3_client.download_file(raster_key, local_raster)

    processor = RasterProcessor(local_raster)
    summary = processor.get_summary()

    print("Raster summary:")
    for k, v in summary.items():
        print(f"{k}: {v}")

    processor.plot_and_save_band(local_png)

    upload_key = local_png
    # throws AccessDenied error, most likely need to set up AWS identity credentials and get PutObject permission to write to s3 bucket
    s3_client.upload_file(local_png, upload_key)
    print(f"Plot uploaded to S3 at: {upload_key}")


if __name__ == "__main__":
    main()

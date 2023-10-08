#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", group="eda", job_type="basic_cleaning", save_code=True)
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    logger.info("Data downloaded")
    ######################
    # YOUR CODE HERE     #
    ######################
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    df.to_csv(args.output_artifact, index=False)
    logger.info("Clean data written to csv")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)
    logger.info("Artifact logged")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help='input artifact', ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help='output artifact',# INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help='output type',## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help='cleaned data',## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,## INSERT TYPE HERE: str, float or int,
        help='min price value for price column',## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,## INSERT TYPE HERE: str, float or int,
        help='min price value for price column',## INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)

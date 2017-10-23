from scrape import collect_congress, collect_images
from average import average_group
from data import prep_data

if __name__ == "__main__":
  # # scrape names, images, party, years for congress members
  # collect_congress()

  # # download images for congress people
  # collect_images()

  df = prep_data()
  df = df[df["party"].isin(["Democratic", "Republican"])]

  # average_group(df, ["party"])
  # average_group(df, ["party", "wing"])
  # average_group(df, ["wing"])
  # average_group(df, ["year"])
  average_group(df, ["state"])


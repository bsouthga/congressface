from scrape import collect_congress, collect_images
from average import crop_and_center
from data import prep_data

if __name__ == "__main__":
  # # scrape names, images, party, years for congress members
  # collect_congress()

  # # download images for congress people
  # collect_images()

  # crop_and_center("111_rp_az_5_mitchell_harry_200.jpg")

  df = prep_data()
  print(df.head())

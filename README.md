# CeilingNyaa

![old, ceiling cat meme](https://i.imgflip.com/ijwq6.jpg)

Checks [nyaa.si](https://nyaa.si/) at regular intervals for the releases you are waiting for.

If any are found, it opens the magnet link and optionally notifies the user via [Pushbullet](https://pushbullet.com/).


## Getting Started

### Prerequisites
```
* Python 2
* pip
* a torrent client set as default
```

### Installing

First, clone this repository.
```
git clone https://github.com/SurgamIdentidem/CeilingNyaa.git
```

Next, navigate into it and install the required packages.
```
cd CeilingNyaa/
pip install -r requirements.txt
```

It should be ready to run.
```
python ceilingnyaa
```


## config.ini

You can edit _config.ini_ to, well, configure the script.

#### [Main]
- **RunOnce**: If True, we will only check for releases once instead of looping. Default: False
- **CheckIntervalInMinutes**: Integer. If _RunOnce_ is False, sets how many minutes to wait in between each loop of checking for new releases. Default: 90
- **WatchListPath**: The path (absolute or relative) to the .csv file containing watchlist data. Default: ../watchlist.csv

#### [PushBullet]
- **NotifyOnNewRelease**: If True, the a notification will be sent to you via Pushbullet. Default: False
- **APIToken**: If _NotifyOnNewRelease_ is True, this token must be set.

#### [Download]
- **AutomaticallyDownloadOnNewRelease**: If True, new releases are automatically downloaded. Default: True
- **MaximumFileSizeInMB**: Float. Prevents downloading files that exceed this file size. Useful for preventing batches. Remove this or set it to 0 to disable checking file sizes.

#### [Logging]
- **ConsoleLogLevel**: Set to 0 to output nothing to the console, 1 for only errors, 2 for errors and successes, and 3 for all. Default: 3
- **FileLogLevel**: Similar to _ConsoleLogLevel_ but applies to the log file being written.


## watchlist.csv

A comma-delimited file containing information about the shows we are awaiting releases for. The first row will be ignored if the first column says _#TITLE_.

* **Title (column 1)**: The title of the show. Please keep entries here unique.
* **Search Terms (column 2)**: The string you would use when searching for this at nyaa.si.
* **Last Known Filename (column 3)**: The last filename you downloaded for this show. This is what the script uses to tell if a new release has come out. It should be noted that, in the unlikely event more than one release comes out since the last check for the same show, only the latest will be "seen" by the script.
* **Categories (column 4, optional)**: The category. The format is x_y where x is the category (e.g. 1 = anime) and y is the subcategory (e.g. 2 = English-translated). 0_0 fetches from all categories and is the default.
* **Filters (column 5, optional)**: The filter. 0 = no filter, 1 = no remakes, 2 = trusted only. Default: 0

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

* [nyaa.si](https://nyaa.si/) for carrying on the torch of nyaa.se.
* [Crunchyroll](http://www.crunchyroll.com/) for making me start following seasonal Japanese cartoons instead of just marathoning and for encouraging me to give them money by having their region blocking lax enough that a simple Chrome extension can bypass said blocking.
* [PyTsada](https://www.facebook.com/groups/itgpytsada/). Just by being in it, it pressures me to relearn Python every once in awhile.

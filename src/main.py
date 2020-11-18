from scraper import Scraper
from config import Config
from mongo import Database


def main() -> None:
    cfg = Config()

    db = Database(cfg)
    db.start(confirm=True)

    sc = Scraper(config=cfg, database=db)
    sc.start()


if __name__ == "__main__":
    main()

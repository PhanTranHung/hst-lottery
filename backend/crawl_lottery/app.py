from flask import Flask, request, jsonify
from pymongo import MongoClient
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from crawler.lottery_spider import LotterySpider
from crawler.constants import valid_channels
import datetime
import config
from crawler import lottery_scraper


app = Flask(__name__)

# MongoDB connection
client = MongoClient(config.MONGO_URI)
db = client.lottery_db


# @app.route('/craw', methods=['GET'])
# def craw_lottery_results():
#     channels = request.args.get('channels')
#     date = request.args.get('date')

#     if not channels or not date:
#         return jsonify({"success": False, "error": "Missing required parameters."}), 400

#     try:

#         # Convert the date string to a datetime object
#         # Validate date format
#         date = datetime.datetime.strptime(date, '%d-%m-%Y')

#         # Split channels into a list
#         channel_list = channels.split(',')
#         for channel in channel_list:
#             if channel not in valid_channels:
#                 return jsonify({"success": False, "error": f"Channel '{channel}' does not exist."}), 400

#         settings = get_project_settings()
#         settings.set("LOG_ENABLED", False)

#         # Start Scrapy crawler
#         process = CrawlerProcess(settings)
#         process.crawl(LotterySpider, channels=channel_list, date=date, db=db)
#         process.start()

#         return jsonify({"success": True}), 200
#     except ValueError:
#         return jsonify({"success": False, "error": "Invalid date format. Use dd-mm-yyyy."}), 400
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

@app.route('/craw', methods=['GET'])
def craw_lottery_results():
    channels = request.args.get('channels')
    date = request.args.get('date')

    if not channels or not date:
        return jsonify({"success": False, "error": "Missing required parameters."}), 400

    try:

        # Convert the date string to a datetime object
        # Validate date format
        date = datetime.datetime.strptime(date, '%d-%m-%Y')

        # Split channels into a list
        channel_list = channels.split(',')
        
        for channel in channel_list:
            if channel not in valid_channels:
                return jsonify({"success": False, "error": f"Channel '{channel}' does not exist."}), 400

        lottery_scraper.scrape_minh_ngoc(channel_list[0], date)

        return jsonify({"success": True}), 200
    except ValueError:
        return jsonify({"success": False, "error": "Invalid date format. Use dd-mm-yyyy."}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host=config.SYSTEM_HOST, port=config.SYSTEM_PORT)

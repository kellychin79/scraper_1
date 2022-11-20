## Goal
This repo is to automatically fetch a product's price online and then send it out to targeted people daily.

Product link: https://www.formbot3d.com/products/voron-24-corexy-3d-printer-kit-with-different-print-sizes-for-choice


### Scraper
I used `selenium` to automate browsers a.k.a Google Chrome will open and close by itself. 
While the browser is open, I used `BeautifulSoup` to scrape the product data, including name, model, stock quantity and current pricing.
After trying a few ideas on how to present the output, I decided to write the result into a txt file in CSV format (the delimiter is comma).
Running below command in the terminal succesfully returned the output in txt file.
> Kellys-Air:scraper_1 kelly$ python3 price_scraper.py

### Scheduler
It took me a long time to figure out the cron job.

Because cron doesn't run commands using a terminal we open so I redirected the output via `> ~/code/scraper_1/result2.txt`.

As the destination of the output of an error, `stderr.log` was helpful for me to find out the reason that the output didn't show up in the txt file.
> Traceback (most recent call last):
  File "price_scraper.py", line 3, in <module>
    from bs4 import BeautifulSoup as bs
ImportError: No module named bs4

I tried to add the install comment at the beginning of the script. It failed because `pip` is for command line and not Python Shell.
> File "price_scraper.py", line 3
    pip3 install bs4 
               ^
SyntaxError: invalid syntax

Later, I identified the issue - it was casued by the cron initially set at `/usr/bin/python3` following some instructions online. cron's environment is different than the one of my terminal. Typing `which python` showed that my terminal used `/opt/anaconda3/bin/python` instead. After updating the cron job content, the script successfully runs automatically.

In summary, I used `crontab -e` to schedule a cron job to run the scraper script every day at 2 pm EST. In the terminal, we can use `crontab -l` to examin the crontab contents.
> 0 19 * * * cd ~/code/scraper_1 && /opt/anaconda3/bin/python price_scraper.py > ~/code/scraper_1/results.txt 2> ~/code/scraper_1/stderr.log

### Delivery
There are many online tutorials explaining how to send email with Python. Three main issues that I encountered are as follows:
- `ModuleNotFoundError: No module named 'email.mime'; 'email' is not a package`: Solved by renaming the file name from email.py to something else. Because `email` is an existing Python package, a file having the same name would cause confusion to the interpreter between user declared module and pre-defined modules.
- Login password: Google doesn't let us sign in to our Google Account from apps on devices that don't support 2-Step Verification. Instead, application-specific password is required.
- I don't want to attach an ugly txt file. And a stackoverflow post inspired me to print the table directly in the email body. Selecting the alternative type gives the flexibility for the receiver to read in an html-aware mail or plain-text reader. Also, make sure the object fed into `tabulate` is a list of list (row) instead of string.

In summary, I used `crontab -e` to schedule a cron job to run the delivery script every day at 2:05 pm EST. In the terminal, we can use `crontab -l` to examin the crontab contents.
> 5 19 * * * cd ~/code/scraper_1 && /opt/anaconda3/bin/python send_email_content.py  2> ~/code/scraper_1/stderr_email.log
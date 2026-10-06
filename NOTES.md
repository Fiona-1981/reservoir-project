Back in spring 2026 (I don't think it was spring 2025), I was getting 
emails from United Utilities warning of low reservoir levels due to the 
recent lack of rainfall. Then we had the multiple heat waves and drought 
of summer 2026, I was made redundant and wanted to build something to 
pull this reservoir data, and present it to a front end. I found Environment 
Agency APIs, but they didn't have reservoir levels - these are down to 
the water companies. This meant scraping and I haven't scraped before. 
It sounds a bit brittle and unreliable, but I thought I'd give it a go 
here anyway. 

I've had some good chats with Claude, and it has suggested beautifulsoup4 
for parsing. From pypi.org:
"Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree."
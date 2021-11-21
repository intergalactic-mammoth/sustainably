<img width="200" alt="portfolio_view" src="https://github.com/intergalactic-mammoth/sustainably/blob/main/readme_media/dashboard.gif">

# Sustainably

Everyone wants to do and be good. Being good feels good. But, sometimes it just takes so much time.

Time for some change!

<img width="200" alt="portfolio_view" src="https://user-images.githubusercontent.com/27728103/142754369-231cfa5b-ff9a-46f1-b389-cae083b8de5c.png">

**sustainably** is a web-app built to empower individuals to achieve their sustainability goals by leveraging state of the art technologies and a simple, intuitive UI/UX. Acknowledging the role individuals in our strive for a cleaner future, our aim is to reduce the gap between consumers and their accessibility to information regarding the life cycle of the prodcuts they purchase. Access to objective information in the palm of their hands, a simple barcode scan way reduces the effort required from individuals and allows them to make informed consumption choice.

**sustainably** leverages computer-vision techniques to identify products and provides concise information related to a product's carboon footprint, recyclability, country of origin, etc. Users can choose to track their own consumption footprint throught the application and in future iterations, get recommendations for their purchasing decisions.

Take a look at these YouTube demos!


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ilZWYAFwbyI/0.jpg)](https://www.youtube.com/watch?v=ilZWYAFwbyI)

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/RlHr6xW_9A0/0.jpg)](https://www.youtube.com/watch?v=RlHr6xW_9A0)

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/2IFigw1aggE/0.jpg)](https://www.youtube.com/watch?v=2IFigw1aggE)


## Local Build/Run Instructions 

### Front-end
#### Requirements
 - jekyll: https://jekyllrb.com/docs/installation/
#### Build and Run Locally
```shell
# install dependencies
bundle install

# run client
bundle exec jekyll serve
```
Back-end
#### Requirements
 - python 3: https://www.python.org/downloads/
 - gunicor: https://docs.gunicorn.org/en/stable/install.html
#### Build and Run
```
#install requirements
pip3 install -r backend-service/requirements.txt

# run
sudo gunicorn -w 4 -b localhost:8080 app:app &
```

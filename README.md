Instructions for Requesting Data:
1.	Prepare the quote_request.txt File:
      The microservice reads requests from a file named quote_request.txt. To request a quote, write a line in this file. The format depends       on the type of quote you're requesting:
    
  	      For a specific topic: Write Topic [Your_Topic]. Replace [Your_Topic] with the desired topic.
  	      For a specific medium: Write Medium [Your_Medium]. Replace [Your_Medium] with the desired medium.
  	      For a random quote: Write Random.
2.	Example Calls:
      o	Request a quote on a specific topic: echo "Topic Love" > quote_request.txt
  	o	Request a quote from a specific medium: echo "Medium Movies" > quote_request.txt
  	o	Request a random quote: echo "Random" > quote_request.txt

Instructions for Receiving Data:
1.	Read the quote_sent.txt File:
      o	Once the microservice processes your request, it writes the selected quote to a file named quote_sent.txt.
      o	Read the contents of this file to see the quote.
      o	Example: cat quote_sent.txt


<img width="813" alt="image" src="https://github.com/mumenr-glitch/app_note/assets/98732876/dda4dc9d-f04e-43dc-beaa-8801fcd3f688">

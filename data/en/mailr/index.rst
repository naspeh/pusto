Welcome to Mailr
================
**Mailr** is an Open Sorce webmail client with gmail like conversations.

**Note.** Mailr is at the beginning of development. There is a lot of work, that has to be 
done.

Source code available on `github. <https://github.com/naspeh/mailr>`_

A big piece of work I did, but it's mostly invisible part and about IMAP communication, 
async synchronization, email parsing. The visible part is some working interface. There is 
`public demo`__, which works pretty fast in reading mode, but you need to be patient if 
pressing "Read", "Archive", "Delete" buttons (and yes, it is not available to compose 
email yet). You can send email to **mailr[at]pusto.org** and it probably appears in Inbox.

__ http://mail.pusto.org

Screenshot
----------

.. image:: screenshot-s.png


Vision of first version
-----------------------
Mailr will have web interface, which will be fast and useful on laptop with small screen, 
on big monitor and on iPad Mini (these devices I have and I want a one customizable web 
interface for them).

Mailr will have gmail compatible mode (through IMAP), so return to gmail will be easy. I 
will also not plan to implement a phone version and this mode can be used in parallel with 
any phone client which connects to gmail as usual. That is also easier to develop using 
gmail as the first backend.

Mailr will have many features from gmail, such as: useful conversations, labels, fast 
search, filters for sorting incoming messages, detecting and folding quotes, keyboard 
shortcuts, SSL support...

Also Mailr will have some additional features.

**Merging conversations.** I really like gmail conversations, they have made the best 
implementation (I have tried many others, when I wanted to move away from gmail). Google 
are matching well which message belongs to which tread, but sometimes they can't match:

.. image:: unmatched-thread.png

I think possibility to merge it manually is a good solution in such cases.

**Write in Markdown.** I like Markdown__ and reStructuredText__ and I want to use them for 
writing my emails. They are also useful for reading after converting to HTML.

__ http://en.wikipedia.org/wiki/Markdown
__ http://en.wikipedia.org/wiki/ReStructuredText

**Two panels.** I really like two panel mode in my VIM(text editor), I started using them 
and now I feel uncomfortable in one panel editor. Second panel gives me more context when 
I write in another one. This feature is in progress, as you can see on the screenshot. But 
I need to implement a possibility to turn that feature off, because I understand, that not 
all people would like it.

**Customizable interface.** As I said Mailr will be useful in different resolutions and 
custom themes and settings for interface will solve this task.

**All in one tab.** I use Chrome and I like that "Settings", "Downloads", "Extensions" 
just open in new tabs instead of new windows (I used Firefox before and it has been using 
new separated windows for those things). I really like consistent user interface. All my 
surfing lives in one window and I want all my emails would probably live in one tab (that 
also means different accounts, but multiple accounts probably will appear after the first 
version).

**Simple backup.** Mailr will have ability to get all your data (including accounts, 
filters, etc.) and restore it on your own server or on secure server of your trusted 
friend.

Next versions
-------------
After I'm able to use Mailr with gmail as backend I want to get the possibility to move 
away from gmail and to switch on my own email address, that mean I probably add support 
Mailgun__ (it is a hard way to support your own mail server with spam filter, so Mailgun 
is easier way to get my own email and they don't save emails in their servers).

__ http://www.mailgun.com/

Then there are many things to keep in mind such as multiple accounts, support other IMAP 
servers, PGP encryption, mailinglists...

Technologies
------------
I want to use minimal scope of dependencies for building Mailr. And I always want to keep 
in mind simplicity when developing it.

- **Python 3** with the help of werkzeug, jinja2, sqlalchemy, lxml;
- **PostgreSQL** with his awesome data types;
- lessjs, jquery(yet only) on the frontend.

**Note:** copy for history from [bountysource][bounty].

[bounty]: https://www.bountysource.com/teams/naspeh/fundraiser

**Open Source webmail client with Gmail-like conversations.**

    With the right instruments
    Folowing the right way
    You can reach big results
    Not so far away

    -- Grisha aka naspeh

I love Open Source. I love emails.

I've been using Gmail during the last seven years. I tried to abandon many times, but always returned. I tried probably all possible alternatives and nothing could fit me as the best conversations made by Google.

I started Mailr few months ago and it already has a pretty good **[public demo][demo]** with narrow feature set. I can read all my emails through Mailr interface and I really like it (sure, because I've been making it). I want to build the first powerful version in **five months** for replacing Gmail in my daily using.

[demo]: http://mail.pusto.org

Code is available on [github][gh] and is first introduced [here][intro] (it is still useful for additional information).

[gh]: https://github.com/naspeh/mailr
[intro]: http://pusto.org/en/mailr/

![Mailr Screenshot](http://pusto.org/en/mailr/screenshot-xs.png)
![Mailr Screenshot](http://pusto.org/en/mailr/screenshot-s.png)

The main principle of Mailr is **simplicity**.

 - simple, but flexible and useful interface
 - codebase created with simplicity in mind (less dependencies, less code - means simplier    for maintaining in the future)
 - simple installation and deployment

When I need only a browser for webmail that's amazing. I have several daily used devices: laptop with small screen for all my work, iPad Mini for reading and surfing. So I want Mailr to be really suitable for small screens and for big monitors as well (I have a big one for testing, but usually watch movies on it).

Why do I think I can do this?
-----------------------------
1. **Right instruments**

   **Python** is really the right language. I love Python. It has a powerful standard    library and lots of useful third party libraries, that give us the power. [Mailpile][mp] and    [InboxApp][inboxapp] both have been made using Python.

[mp]: https://www.mailpile.is/
[inboxapp]: https://www.inboxapp.com/

   **PosgresSQL** is the right storage. It can be used with transactions, replications and    backups for saving my emails carefully. It has a useful feature set for searching and    indexing, so I don't need to reinvent the wheel for these things. All emails with    attachments are in the database, so just a simple backup and all my data is with me    again.

   **Less** is used instead of CSS for better theming.

2. **Right way** (for getting the first usable version as soon as possible)

   **Gmail** is used as the first backend through IMAP with bidirectional synchronization. Gmail has a good storage for emails, filters for incoming messages, powerful spam    filter, email clients for smartphones and tablets. And I always can return to Gmail    again and use it as usual or just use it in parallel mode.

   So with Gmail I can do most important features first and some can wait. I can already read emails through Mailr, the next feature is writing emails. And I need to implement,    optimize, and polish a big set of features: conversations, email parsing,    synchronizing, search, detecting and folding quotes, hotkeys, settings, themes, label    handling, filtering of incoming messages, SSL support, etc.

   **Mailgun** will be used as the second backend. Setting up and supporting my own email    server with good spam filter and good reliability is a horrible thing. So services like    Mailgun can help me with this stuff.

   If I implement Mailgun and make good replication for my PosgreSQL I will be able to    remove synchronization with Gmail from my usage. That will simplify and speed up Mailr    installation, because synchronization part is always complicated and can be slow    sometimes.

   **Other IMAP servers** afterwards (so that Mailr could be used with my own full setup).

I need $15,000 for five months of my work
-----------------------------------------
I will work full-time on Mailr in two iterations (each in two and half months).

The first iteration named "I've moved away from Gmail but with Gmail behind my back":

 - composing and sending email
 - improving conversation with all important actions
 - improving and optimizing synchronization through IMAP
 - improving email parsing
 - improving detecting and folding quotes and signatures
 - improving database schema
 - preparing docker image and ansible playbook (for simple installation)
 - preparing instructions for installation
 - publishing

After the first iteration I suppose I will switch to Mailr on daily basis.

Second iteration, named "Really, I have moved away from Gmail!"

 - improving and optimization of all existing features
 - improving user interface and themes
 - filtering incoming messages
 - multi-account support (one tab for all email accounts)
 - Mailgun support
 - preparing some documentation
 - publishing

After the second iteration I expect Mailr to be a perfect alternative for webmail.

Who am I?
---------
My name is Grisha Kostyuk aka naspeh. My email is naspeh[at]gmail.com. I was born on Apr 15, 1983. I'm a passionate programmer from Ukraine with experience of about seven years in web development, more than four last years with Python. I usually work as full-stack web developer on full-time position (often remote).

Why fundraiser?
---------------
Since April 2013 I have spent my time mostly on my own projects (including my newborn first son). Mailr is the last thing I have been working on during the recent four months, including research, first prototype (which I gave up) and start of developing Mailr from scratch (current version took about two months and half).

Now I have spent almost all the money I had (I haven't earnt anything since April 2013) and I need to get a job for supporting my family. But I want to develop Mailr. Now I'm deep in the context of Mailr, I have a lot of enthusiasm and this is the right time, because if I get a job I will dive deep in a new role and a new project and Mailr may be late for about year. So I really want to work on email stuff and I need some money.

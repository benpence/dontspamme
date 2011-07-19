## DONTSPAMME

__dontspamme__ is an anti-spam, anonymous remailer tool for Google users.
### How does it work?
__dontspamme__ enables you to monitor and control how your email identity propagates. For this explanation, let _someSite.com_ represent a website. When _someSite.com_ requests your email address, you create a unique ‘Pseudonym’ that stealthily links back to your email address. This Pseudonym is simply a relay between your _@gmail.com_ account and someSite.com. When _someSite.com_ sends an email to your Pseudonym, it is relayed to your _@gmail.com_. When you send an email to your Pseudonym, it is relayed back to _someSite.com_:

![Concept Image](http://www.likeitmatters.com/wp-content/uploads/2011/07/blog-dontspamme-1.png)

This concept is [anonymous remailing](http://en.wikipedia.org/wiki/Anonymous_remailer). How does this help you avoid SPAM? When you create the Pseudonym, it is tied to _someSite.com_. Assume you have created a Pseudonym a5eyz@dontspam.me for _someSite.com_. Suppose _someOtherSite.com_ starts emailing your Pseudonym a5eyz@dontspam.me. You will know immediately that _someSite.com_ gave away your email address and all these emails from _someOtherSite.com_ are SPAM. And by you will know, I mean that the relay in-between will automatically flag or discard (your choice) these suspected SPAM emails.

### How does it really work?
__dontspamme__ runs on Google App Engine. Google App Engine allows you to write scalable web applications that use Google’s datastore. Up to a certain quota of traffic, content size, emails received/sent, it’s free. The __dontspamme __app works as a smart anonymous remailer. For every person that sends an email to the Pseudonym, __dontspamme__ creates a tag so that you can specify the person at _someSite.com_ to whom you want to reply:

![Reply Image](http://www.likeitmatters.com/wp-content/uploads/2011/07/blog-dontspamme-2.png)

### Who is this for?
All Google users.

### How to use
#### Install
Refer to [[Install]]

#### User's guide
Refer to [[User's Guide]]

#### Notes
* Version 11.7 has not been thoroughly tested. Use at your own risk (although the source code's there for you to examine and modify).
* At the time of this writing, the mail API does not work on custom domains.

### Team
* Ben Pence (benpence): developer & idea man
* Alex Levenson (isnotinvain): occasional contributor

Please message someone on the team to get involved.

### License
Read 'LICENSE' in the root directory.
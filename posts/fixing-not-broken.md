title: Fixing Whats not Broken
desc: About making more informed decisions when you decide to refactor things, especially things that are currently working fine
date: 4/30/2015
tags: tech
link: http://lynncyrin.me/post/fixing-not-broken

### [Making Better Decisions about When to Refactor your Code](/post/fixing-not-broken)

<div style="text-align: center;"> <img style="max-width:600px;" src="http://i.imgur.com/qP2hSPf.jpg" alt="A commit message saying 'remove S3 stuff'"></div>

So that, that's the commit message of a developer doing something they probably shouldn't. Like, if you're going to refactor your code to move away from the leading solution for a particular problem, you had better do a lot of thinking on how you are going to do it. I didn't, and made a huge mess. Here's what happened:

<readmore></readmore>

I wanted to move away from using [AWS S3](http://aws.amazon.com/s3) as the image hosting for [Quirell](http://gitlab.com/collectqt/quirell). I still think that reasons are pretty solid

* I want to make it easy for people to create their own version of Quirell, or at least to test the full feature set
* To expidite that, I was going to make sure to eiter include throwaway account credentials (U: THROWAWAY_TEST_ACCOUNT@gmail.com // P: I_really_dont_care_about_this) or make it so that you only have to make one account with a provider that provides a variety of services (which in the case of Quirell, would be [Heroku](http://heroku.com))
* Giving out throwaway account credentials for S3 is impossible since AWS requires a credit card on signup, which also makes getting AWS running at a basic level take more effort than [things that don't require a CC on signup]. Setting up [IAM](http://aws.amazon.com/iam) doesn't really help in this regard.

There are a few other reasons (S3 not being specific to images, and being popular enough that exploits are very well known, ...), but those are the big ones. They seemed like good enough reasons at the time to start looking into alternatives. I started with [Cloudinary](http://cloudinary.com) and ended with...

<div style="text-align: center;"> <img style="max-width:600px;" src="http://i.imgur.com/zlWpJSF.jpg" alt="A commit message saying 'Revert remove S3 stuff'"></div>

...going back to S3. Although it took me about a week's worth of work and a ton of frustration before I went back. Mainly because of 3 issues

* I didn't isolate the system in question (image uploads) from the rest of my application. I should have wrote a unit test with a webdriver like [selenium](http://www.seleniumhq.org) (note: I haven't used Selenium before and I'm not exactly sure how I would write this test), and made sure to be aware of all the parts of my application that deal with image uploads.
* I didn't properly define the system I was implementing. When searching for alternatives I was just thinking I need to do "image uploads" when really what I needed was "signed client side direct uploads". Those being an upload where the client asks your server for a signature so that they can upload to directly to the image server under your name.
* I didn't make sure that the service I'm switching to actually supports the technology I'm using. Specifically, Cloudinary supports Django but not Flask. They're similar enough that you could swap out the Django depedencies for Flask specific or web framework agnostic code, but after about two days of trying to get that to work (again, without tests) I decided it wasn't worth my time.

I'm going to compare to this a relatively simple refactor of swaping [flask-wtf](http://flask-wtf.readthedocs.org/en/latest/) out for [flask-seasurf](http://flask-seasurf.readthedocs.org/en/latest/) for handling CSRF protection. The simplicity of the system was very influential, but also I knew beforehand that:

* I could write a fairly straightforward test that looks for a 40X HTTP error, thrown when the CSRF validation fails
* I could isolate testing CSRF validation from every other system (without having to learn selenium).
* That CSRF validation is the entirety of what I wanted to accomplish
* Both things work in flask (I mean, it's in the name)

So that refactor was... mostly painless. I ran into an issue where I didn't isolate the system well enough, and it took me about 6 hours figure out what was wrong and whether or not it had to do with the refactor or not. Turns out that it didn't, [and I got a new issue report out of it](https://gitlab.com/collectqt/quirell/issues/176#note_1171370). But all in all, this experience was a ton less stressful than the one with S3 / cloudinary, and primarily for the reasons mentioned above. Hopefully other people will learn from my experience here, and:

* Write tests
* Isolate the system
* Accurately identify the system
* Verify the dependencies

Good luck!

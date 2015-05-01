title: Fixing Whats not Broken
desc: About making more informed decisions when you decide to refactor things
date: 4/30/2015
tags: tech
link: http://lynncyrin.me/post/fixing-not-broken.md

### [Making Better Decisions about When to Fix Things that aren't Broken](/post/fixing-not-broken)

![A commit message saying 'remove S3 stuff'](https://lh6.googleusercontent.com/_vaTKtxAYZA3C7IW3vK9BlF-xbYJFgO7_SUdS13xSm4Bn0socqiIOeeXgtd7Qgf4GrbsNL4zTj2-_vU=w1342-h513)

So that, that's the commit message of a developer doing something they probably shouldn't. Like, if you're going to refactor your code to move away from the leading solution for a particular problem, you had better do a lot of thinking on how you are going to do it. I didn't, and made a huge mess. Here's what happened:

I wanted to move away from using [AWS S3](http://aws.amazon.com/s3) as the image hosting for [Quirell](http://gitlab.com/collectqt/quirell). I still think that reasons are pretty solid

* I want to make it easy for people to create their own version of Quirell, or at least to test the full feature set
* To expidite that, I was going to make sure to eiter include throwaway account credentials (U: THROWAWAY_TEST_ACCOUNT@gmail.com // P: I_really_dont_care_about_this) or make it so that you only have to make one account with a provider that provides a variety of services (which in the case of Quirell, would be [Heroku](http://heroku.com))
* Giving out throwaway account credentials for S3 is impossible since AWS requires a credit card on signup, which also makes getting AWS running at a basic level take more effort than [things that don't require a CC on signup]. Setting up IAM doesn't really help in this regard

![A commit message saying 'Revert remove S3 stuff'](https://lh6.googleusercontent.com/KQa15V4Z8phXX1_9d4cuJ2E_8MZxbkkLMxCw8mYVskyZ2QJ8Qqy32C0pdnTdjYkxMhfLPnyS0QJ4v1E=w1342-h513)

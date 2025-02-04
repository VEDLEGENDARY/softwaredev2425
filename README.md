# Daily Mailer
# Video Demo:  https://youtu.be/YlKeHLdYT94
# Description:

## Problem
It should be effortless for teachers and school administrators to pass information to students in a simple way. Most of the students in the modern-day world do not like reading long emails or keeping up with current events. They just prefer small, quick, and catchy information that comes along while they are browsing through social media sites. Schools require a medium by which updates could be made more interesting to the teachers themselves, which on its own accord could result in keeping students interested in activities.

## Solution

Thus came **The Daily Mailer**! It is a lightweight utility that allows teachers or administrators to email students in a much readable and interactive format. Design your own email templates through the inbuilt rich text editor. These use dynamic variables like `{weather:conditions}` that are filled in with live data at sending time. This assures the emails are always dynamic, contextual, and timeliest, as you might be creating a template only once to then reuse it easily.

Using Daily Mailer, with the help of its AI assistant via GTP-3.5, one will be able to come up with neat email drafts in record time. And this is going to work in a way since teachers will hardly have a spare minute due to being always on the run. A teacher takes the content over the format so as to make the process faster.

Daily Mailer allows the application to design and send customized e-mails to the students. It even provides a rich text editor to style your e-mails with Live Weather Updates, Inspirational Quotes, and many more to make such letters more interesting. Reminders, announcements, and personal messages from the teacher also help the children keep in touch and be interested in the activities in a class.

In addition, if one could save e-mails in some special `.dmail` format, that would allow reusing or even sharing templates with other people. The most important thing, on top of security, is that this system allows sending emails only to trusted users, where each user gets assigned a unique hash ID.

## How It Works

The application usability is very user-friendly; you just input your data and set up APIs via a super-friendly interface. In its further work, the application pulls for you data from other sources, like weather updates or quotes, and injects them into the email templates. This will also enable users to track which students have opened and read their emails, hence offering great insight into engagement.

You can easily move between different parts of this application, like template creation, contact management, and settings changes. For this reason, it becomes quite efficient and time-saving, too, for educators with especially busy schedules. The design is clean and user-friendly; hence, it would be accessible for teachers at any level of computer skills.

## Design Decisions

We had to make a few important decisions during development. We didn't use a heavy WYSIWYG editor but a rich text editor that is far simpler, with good formatting for emails. It kept things lightweight and fast.

First and foremost, we take safety into consideration. So, we did an authentication system based on hash where every user will have a unique hash ID in order to make sure only trusted users will have the possibility of sending emails. Instead of going with cloud storage, we decided to store data locally on the user's device. The whole point was to keep things fast and secure.

On the other important side was GPT 3.5 as an assistant to help users in drafting emails within a very short time. In this way, GPT saves not only a lot of precious time for the teacher but also gives him satisfaction in composing a well-written email rather than spending most of the time drafting it.

## Behind the Scenes

Daily Mailer was written in **PySide6** to get the best results on the front end. That's why it looks so clear and friendly to use. We have installed **Flask** for the back end, as we will have to do things related to HTTP requests or whatever else is associated with APIs. By doing so, this keeps the application flexible and extensible to cope with several users' data more effectively.

Security: The hash-based system ensures that only authenticated users send emails. Identification numbers will identify each of the clients for checking requests. The application shall save all information related to users on the local machine itself in order to assure privacy and speed. Besides, it keeps a record of email usage for providing useful analytics to admins regarding engagements and email activities.

In enhancing the application, the development process has widely tested it for bug detection, performance, and user interface refinement. In the development of the app, resources like ChatGPT were used to help in brainstorming solutions and enhancing the functionality within the app.

## Conclusion

Daily Mailer is that one-of-a-kind, powerful communication and emailing tool that modern teacher and school management can avail themselves with respect to communicating with students. The facility allows for designing dynamic emails and sending them to the target list of people. The application allows one to do AI-assisted email drafting, live data updates, and safe local storage for making emailing quicker and enjoyable. We really are excited to open those new horizons, which Daily Mailer will open for enhancing school communication and transforming it into some sort of interactivity. Thus, letting the teachers teach while taking care of the rest surely classifies it as one of the must-have modern education tools.

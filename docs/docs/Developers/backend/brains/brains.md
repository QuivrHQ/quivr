---
sidebar_position: 1
---

# Introduction to Brains

Quivr has a concept of "Brains". They are ring fenced bodies of information that can be used to provide context to Large Language Models (LLMs) to answer questions on a particular topic.

LLMs are trained on a large variety of data but to answer a question on a specific topic or to be used to make deductions around a specific topic, they need to be supplied with the context of that topic.

Quivr uses brains as an intuitive way to provide that context.

When a brain is selected in Quivr, the LLM will be provided with only the context of that brain. This allows users to build brains for specific topics and then use them to answer questions about that topic.

In the future there will be the functionality to share brains with other users of Quivr.

## How to use Brains

To use a brain, simply select the menu from using the Brain icon in the header at the top right of the Quivr interface.

You can create a new brain by clicking the "Create Brain" button. You will be prompted to enter a name for the brain. If you wish you can also just use the default brain for your account.

To switch to a different brain, simply click on the brain name in the menu and select the brain you wish to use.

If you have not chosen a brain, you can assume that any documentation you upload will be added to the default brain.

**Note: If you are having problems with the chat functionality, try selecting a brain from the menu. The default brain is not always selected automatically and you will need a brain selected to use the chat functionality.**

## Using Resend API

We have integrated [Resend](https://resend.com/docs/introduction), an email API for developers, in our application to handle sharing brains with an email invitation.

Two environment variables have been introduced to handle this integration:

- RESEND_API_KEY: This is the unique API key provided by Resend for our application. It allows us to communicate with the Resend platform in a secure way.

- RESEND_EMAIL_ADDRESS: This is the email address we use as the sender address when sending emails through Resend.

After fetching our Resend API key and email address from environment variables, we use it to send an email via resend.Emails.send method.

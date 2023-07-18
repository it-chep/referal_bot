Referal bot
This is a referral bot on the telegram channel.

Administration of all referrals is in django admin.

Implemented api connection with the salebot constructor

The logic of the referral system is as follows:

The user enters the channel with an invite link. The bot on salebot is the first to send him a message stating that the user can receive a gift and fit into the referral system.

After the user has received the messages, the referral bot on Django (DjangoBot) adds it to the channel's user base so that it cannot give a bonus to the inviter 2 times.

Also, DB will remember the invitation links of all users and for reaching n the number of invited guests, a bonus will be issued to the inviter

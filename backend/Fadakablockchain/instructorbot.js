const { ActivityHandler, BotFrameworkAdapter } = require('botbuilder');

class InstructorBot extends ActivityHandler {
constructor() {
super();
this.onMessage(async (context, next) => {
await context.sendActivity(`You asked about '${context.activity.text}'. Let me help you with that.`);
await next();
});
}
}

const adapter = new BotFrameworkAdapter({
appId: process.env.MicrosoftAppId,
appPassword: process.env.MicrosoftAppPassword
});

const bot = new InstructorBot();
adapter.processActivity(req, res, async (context) => {
await bot.run(context);
});

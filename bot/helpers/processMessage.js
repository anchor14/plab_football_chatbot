const API_AI_TOKEN = 'f6b62ed5a54d42abace1504906fc9d44';
const apiAiClient = require('apiai')(API_AI_TOKEN);

const FACEBOOK_ACCESS_TOKEN = 'EAAE9fTjEypcBAPN5P8w2zzj3qDwyQR1BL1SMqQP6jAjZA60mNMc12ZCMbZC9y19MpLiVePA6eYhcZBZBNxT5LITAPC0MpXPBkjsdT98MX8pTFlWFd2m2SML0yCZCw5Oi7rigBnOOZB9LX2xsguoxG4V1YhZAKpkclvU7gpVLUbZB4wwZDZD';
const request = require('request');

const sendTextMessage = (senderId, text) => {
  request({
    url: 'https://graph.facebook.com/v2.6/me/messages',
    qs: { access_token: FACEBOOK_ACCESS_TOKEN },
    method: 'POST',
    json: {
      recipient: { id: senderId },
      message: { text },
    }
  });
};

module.exports = (event) => {
  const senderId = event.sender.id;
  const message = event.message.text;

  const apiAiSession = apiAiClient.textRequest(message, {sessionId: 'crowdbotics_bot'});

  apiAiSession.on('response', (response) => {
    const result = response.result.fulfillment.speech;

    sendTextMessage(senderId, result);
  });

  apiAiSession.on('error', error => console.log(error));
  apiAiSession.end();
};

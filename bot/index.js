const express = require('express');
const bodyParser = require('body-parser');

const app = express();

var url = 'http://127.0.0.1:5000/';


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true}));

const verificationController = require('./controllers/verification');
const messageWebhookController = require('./controllers/messageWebhook');

app.get('/', verificationController);
app.post('/', messageWebhookController);

app.listen(3000, () => console.log('Webook server is listening, port 3000'));

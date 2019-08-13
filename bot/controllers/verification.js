module.exports = (req, res) => {
  const hubChallenge = req.query['hub.challenge'];

  const hubMode = req.query['hub.mode'];
  const verifyTokenMathces = (req.query['hub.verify_token'] ==='crowdbotics');

  if (hubMode && verifyTokenMathces) {
    res.status(200).send(hubChallenge);
  } else {
    res.status(403).end();
  }
};

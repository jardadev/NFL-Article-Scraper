const express = require('express');
const app = express();
const { run } = require('./server');


app.listen(3000, () => console.log('Server ready'));
run();
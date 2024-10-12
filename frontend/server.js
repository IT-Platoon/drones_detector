const express = require('express');
const serveStatic = require("serve-static")
const cors = require("cors");
const path = require('path');
app = express();

app.use(serveStatic(path.join(__dirname, 'dist')));
app.use(cors({
    origin: 'http://localhost:8080',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'],
    allowedHeaders: ['Content-Type'],
}))
const port = process.env.PORT || 3000;
app.listen(port);

const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];
const last1000 = line78.slice(-1000);
console.log('Last 1000 chars:');
console.log(last1000);
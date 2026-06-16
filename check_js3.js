const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const first100 = line78.slice(0, 100);
console.log('First 100 chars:', first100);

const colonCount = (line78.match(/:/g) || []).length;
const quoteCount = (line78.match(/"/g) || []).length;
console.log('Colon count:', colonCount);
console.log('Quote count:', quoteCount);

const equalsPos = line78.indexOf('=');
console.log('First = position:', equalsPos);

const commaPos = line78.lastIndexOf(',');
console.log('Last , position:', commaPos);
console.log('Chars after last comma:', line78.slice(commaPos + 1));
const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const redmojiIndex = line78.indexOf('"redmoji":');
console.log('Line 78 content:', line78.length, 'chars');

const afterRedmoji = line78.slice(redmojiIndex);
console.log('After redmoji:', afterRedmoji.length, 'chars');

const firstColon = afterRedmoji.indexOf(':');
const firstQuote = afterRedmoji.indexOf('"', firstColon + 1);
const secondQuote = afterRedmoji.indexOf('"', firstQuote + 1);

console.log('First colon at:', firstColon);
console.log('First quote at:', firstQuote);
console.log('Second quote at:', secondQuote);

const pattern = /"redmoji": "\{.*\}"$/;
if (pattern.test(line78)) {
    console.log('Pattern matches!');
} else {
    console.log('Pattern does NOT match!');
    console.log('Line 78 ends with:', JSON.stringify(line78.slice(-20)));
}

const lastQuote = line78.lastIndexOf('"');
const lastColon = line78.lastIndexOf(':');
const lastComma = line78.lastIndexOf(',');

console.log('Last quote at:', lastQuote);
console.log('Last colon at:', lastColon);
console.log('Last comma at:', lastComma);

if (lastQuote > lastColon) {
    console.log('Last quote is after last colon - string ends properly');
} else {
    console.log('Last colon is after last quote - POSSIBLE ISSUE!');
}

if (lastComma < lastColon) {
    console.log('Last comma is before last colon - POSSIBLE MISSING COMMA!');
}
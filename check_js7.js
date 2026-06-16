const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const redmojiIndex = line78.indexOf('"redmoji":');
const jsonStart = redmojiIndex + 10 + 2;
const jsonEnd = line78.lastIndexOf('"}') + 1;

const jsonStr = line78.slice(jsonStart, jsonEnd);
const unescaped = jsonStr.replace(/\\"/g, '"');

const errorPos = 39140;
const start = Math.max(0, errorPos - 100);
const end = Math.min(unescaped.length, errorPos + 100);

console.log('Context around error:');
console.log(unescaped.slice(start, end));
console.log('');
console.log('Position in context:', errorPos - start);

let i = errorPos;
while (i >= 0 && unescaped[i] !== '"') {
    i--;
}
const keyStart = i + 1;
i = errorPos;
while (i < unescaped.length && unescaped[i] !== ',' && unescaped[i] !== '}') {
    i++;
}
const valueEnd = i;

console.log('');
console.log('Key:', unescaped.slice(keyStart, keyStart + 50));
console.log('Value:', unescaped.slice(errorPos, Math.min(errorPos + 100, unescaped.length)));
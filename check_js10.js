const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const redmojiIndex = line78.indexOf('"redmoji":');
const valueStart = redmojiIndex + 10 + 2;

const jsonStr = line78.slice(valueStart, line78.length - 3);

console.log('jsonStr length:', jsonStr.length);
console.log('First 100:', jsonStr.slice(0, 100));
console.log('Last 100:', jsonStr.slice(-100));

try {
    const parsed = JSON.parse(jsonStr);
    console.log('Direct parse success!');
    console.log('Type:', typeof parsed);
} catch (e) {
    console.log('Direct parse error:', e.message);
}

const unescaped = jsonStr.replace(/\\"/g, '"');
console.log('');
console.log('unescaped length:', unescaped.length);
console.log('First 100:', unescaped.slice(0, 100));
console.log('Last 100:', unescaped.slice(-100));

try {
    const parsed = JSON.parse(unescaped);
    console.log('Unescaped parse success!');
    console.log('redmojiTabs:', parsed.redmojiTabs?.length);
    console.log('redmojiMap keys:', Object.keys(parsed.redmojiMap || {}).length);
} catch (e) {
    console.log('Unescaped parse error:', e.message);
    const errorPos = parseInt(e.message.match(/position (\d+)/)?.[1] || '0');
    console.log('Error position:', errorPos);
    console.log('Context around error:');
    console.log(unescaped.slice(Math.max(0, errorPos - 30), Math.min(unescaped.length, errorPos + 30)));
}
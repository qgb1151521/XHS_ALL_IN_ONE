const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const redmojiIndex = line78.indexOf('"redmoji":');
console.log('redmoji index:', redmojiIndex);

const afterRedmoji = line78.slice(redmojiIndex + 10);
console.log('After "redmoji":', afterRedmoji.slice(0, 50));

const firstQuote = afterRedmoji.indexOf('"');
console.log('First quote after redmoji:', firstQuote);

const jsonStart = redmojiIndex + 10 + firstQuote + 1;
console.log('JSON start index:', jsonStart);

let depth = 0;
let jsonEnd = -1;
let inString = false;
let escape = false;

for (let i = jsonStart; i < line78.length; i++) {
    const char = line78[i];
    
    if (escape) {
        escape = false;
        continue;
    }
    
    if (char === '\\') {
        escape = true;
        continue;
    }
    
    if (char === '"') {
        inString = !inString;
        continue;
    }
    
    if (!inString) {
        if (char === '{') {
            depth++;
        } else if (char === '}') {
            depth--;
            if (depth === 0) {
                jsonEnd = i;
                break;
            }
        }
    }
}

console.log('JSON end index:', jsonEnd);
console.log('JSON length:', jsonEnd - jsonStart + 1);

const jsonStr = line78.slice(jsonStart, jsonEnd + 1);
try {
    const parsed = JSON.parse(jsonStr);
    console.log('JSON parse success!');
    console.log('redmojiTabs count:', parsed.redmojiTabs?.length);
    console.log('redmojiMap keys count:', Object.keys(parsed.redmojiMap || {}).length);
} catch (e) {
    console.log('JSON parse error:', e.message);
    console.log('First 200 chars of JSON:', jsonStr.slice(0, 200));
    console.log('Last 200 chars of JSON:', jsonStr.slice(-200));
}
const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const redmojiIndex = line78.indexOf('"redmoji":');
const valueStart = redmojiIndex + 10 + 2;

const jsonStr = line78.slice(valueStart, line78.length - 3);

const unescaped = jsonStr.replace(/\\"/g, '"');

let depth = 0;
let inString = false;
let escape = false;
let key = '';
let expectColon = false;
let errors = [];

for (let i = 0; i < unescaped.length; i++) {
    const char = unescaped[i];
    
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
        if (!inString && key) {
            expectColon = true;
        }
        continue;
    }
    
    if (!inString) {
        if (char === '{') {
            depth++;
            expectColon = false;
        } else if (char === '}') {
            depth--;
            expectColon = false;
        } else if (char === ':') {
            if (!expectColon && depth > 0) {
                errors.push({ pos: i, msg: 'Unexpected colon', context: unescaped.slice(Math.max(0, i - 20), i + 20) });
            }
            expectColon = false;
        } else if (char === ',') {
            expectColon = false;
        } else if (char !== ' ' && char !== '\t') {
            if (expectColon) {
                errors.push({ pos: i, msg: 'Expected colon after key', context: unescaped.slice(Math.max(0, i - 20), i + 20) });
            }
        }
    }
}

if (depth !== 0) {
    errors.push({ pos: unescaped.length, msg: 'Unbalanced braces, depth: ' + depth });
}

console.log('Total errors:', errors.length);
errors.forEach((e, idx) => {
    console.log(`Error ${idx + 1}: ${e.msg} at position ${e.pos}`);
    console.log(`  Context: ${e.context}`);
});
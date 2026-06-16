const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const redmojiIndex = line78.indexOf('"redmoji":');
const valueStart = redmojiIndex + 10 + 2;

const jsonStr = line78.slice(valueStart, line78.length - 3);

const quoteCount = (jsonStr.match(/"/g) || []).length;
const escapedQuoteCount = (jsonStr.match(/\\"/g) || []).length;
const unescapedQuoteCount = quoteCount - escapedQuoteCount;

console.log('Total quotes:', quoteCount);
console.log('Escaped quotes:', escapedQuoteCount);
console.log('Unescaped quotes:', unescapedQuoteCount);

if (unescapedQuoteCount > 0) {
    console.log('FOUND UNESCAPED QUOTES!');
    let pos = 0;
    while ((pos = jsonStr.indexOf('"', pos)) !== -1) {
        if (pos > 0 && jsonStr[pos - 1] !== '\\') {
            console.log('Unescaped quote at position:', pos);
            console.log('Context:', jsonStr.slice(Math.max(0, pos - 20), pos + 20));
        }
        pos++;
    }
} else {
    console.log('All quotes are properly escaped');
}
const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const redmojiIndex = line78.indexOf('"redmoji":');
const jsonStart = redmojiIndex + 10 + 2; 
const jsonEnd = line78.lastIndexOf('"}') + 1;

const jsonStr = line78.slice(jsonStart, jsonEnd);

const unescaped = jsonStr.replace(/\\"/g, '"');

try {
    const parsed = JSON.parse(unescaped);
    console.log('JSON parse success!');
    console.log('redmojiTabs count:', parsed.redmojiTabs?.length);
    console.log('redmojiMap keys count:', Object.keys(parsed.redmojiMap || {}).length);
} catch (e) {
    console.log('JSON parse error:', e.message);
    console.log('Error position:', e.message.match(/position (\d+)/)?.[1]);
    
    const errorPos = parseInt(e.message.match(/position (\d+)/)?.[1] || '0');
    const start = Math.max(0, errorPos - 50);
    const end = Math.min(unescaped.length, errorPos + 50);
    console.log('Context around error:');
    console.log(unescaped.slice(start, end));
    console.log('Position:', errorPos - start);
}
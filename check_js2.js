const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const parts = line78.split('":"');
console.log('Number of parts:', parts.length);

for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    const last50 = part.slice(-50);
    const first50 = part.slice(0, 50);
    if (i > 0 && !last50.includes('"')) {
        console.log(`Part ${i}: missing closing quote?`);
        console.log(`  Last 50: '${last50}'`);
    }
    if (i < parts.length - 1 && !first50.includes('"')) {
        console.log(`Part ${i}: missing opening quote?`);
        console.log(`  First 50: '${first50}'`);
    }
}
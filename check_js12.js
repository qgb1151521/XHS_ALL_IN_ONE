const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');

for (let i = 270; i < 275; i++) {
    const line = lines[i];
    console.log(`Line ${i + 1}: ${line.length} chars`);
    console.log(`  First 100: ${line.slice(0, 100)}`);
    console.log(`  Last 100: ${line.slice(-100)}`);
    
    try {
        new Function(line);
        console.log('  Syntax OK');
    } catch (e) {
        console.log('  Syntax error:', e.message);
    }
    console.log('');
}
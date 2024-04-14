import MD5 from './../build/md5-es.min';

const numberWithCommas = (x) => {
    const parts = x.toString().split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return parts.join('.');
};

process.stdout.write('\u001B[2J\u001B[0;0f');
console.log('Running performance tests...');

let i = 0,
    startDate = null,
    dateDiff = null,
    rate = null,
    MD5Rate = null;

const length = 5000000;

// 1st allocation
MD5.hash('allocate');

i = 0;
startDate = new Date();
for (i; i < length; i++) {
    MD5.hash(i.toString());
}
dateDiff = new Date() - startDate;
rate = (length / dateDiff) * 1000;
MD5Rate = rate;
console.log(`   MD5 rate: ${numberWithCommas(rate.toFixed())} hashes/sec`);

i = 0;
startDate = new Date();
for (i; i < length; i++) {
    MD5.hash(i.toString());
}
dateDiff = new Date() - startDate;
rate = (length / dateDiff) * 1000;
const relativeRate = rate / MD5Rate * 100 - 100;
console.log(`   MD5 rate: ${numberWithCommas(rate.toFixed())} hashes/sec 0.00 (${Math.abs(relativeRate).toFixed(2)}% ${((relativeRate >= 0) ? 'faster' : 'slower')} than first run)`);


console.log('Performance tests ran successfully.');
console.log('');
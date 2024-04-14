import MD5 from './../src/md5';

describe('MD5', () => {
    describe('#hash', () => {
        it('should return hash for a empty string', () => {
            expect(MD5.hash('')).toBe('d41d8cd98f00b204e9800998ecf8427e');
        });
        it('should return hash for strings (1 character)', () => {
            expect(MD5.hash('a')).toBe('0cc175b9c0f1b6a831c399e269772661');
        });
        it('should return hash for strings (3 characters)', () => {
            expect(MD5.hash('abc')).toBe('900150983cd24fb0d6963f7d28e17f72');
        });
        it('should return hash for strings containing spaces', () => {
            expect(MD5.hash('message digest')).toBe('f96b697d7cb7938d525a2f31aaf161d0');
        });
        it('should return hash for strings containing no spaces', () => {
            expect(MD5.hash('abcdefghijklmnopqrstuvwxyz')).toBe('c3fcd3d76192e4007dfb496cca67e13b');
        });
        it('should return hash for strings containing uppercase, lowercase and numericals', () => {
            expect(MD5.hash('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')).toBe('d174ab98d277d9f5a5611c2c9f419d9f');
        });
        it('should return hash for strings containing only numbers (80 characters)', () => {
            expect(MD5.hash('12345678901234567890123456789012345678901234567890123456789012345678901234567890')).toBe('57edf4a22be3c955ac49da2e2107b67a');
        });
        it('should return hash for strings containing only numbers (160 characters)', () => {
            expect(MD5.hash('1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890')).toBe('268c7919189d85e276d74b8c60b2f84f');
        });
        it('should return a hash with length 32 characters', () => {
            const hash = MD5.hash('cryptographic hash function');
            expect(hash.length).toBe(32);
        });
    });
});

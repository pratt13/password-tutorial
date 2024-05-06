# What is a strong password

## Character set
The number of combinations a hacker must try to get your password is given by the permutation with replacement formula:
```
n_P_r = Number of possible passwords = Size of the character set ^ password length
```

So, for a password of length 4, if the password is only allowed to be lowercase alphabet, the number of combinations is
```
n_P_r = 26 ^ 6 = 456976
```

But if uppercase and numbers are allowed

```
n_P_r = (26 + 26 + 10) ^ 6 = 14776336
```

This is why passwords suggest using upper/lower/numeric and special characters to increase complexity.

## Entropy
Entropy in general, is a measure of disorder of a system, high entropy means there is less order.
As such entropy is useful as a measure for hwo good a password is, high entropy would mean it is harder to guess as it is less predictable.
High entropy is good, low entropy is bad.
Google has further details, but [nord](https://nordvpn.com/blog/what-is-password-entropy/#:~:text=You%20can%20calculate%20password%20entropy,password%20entropy%2C%20measured%20in%20bits.) is pretty good.

Computing entropy
Log2(number of characters ^ length of password)

* Log2 is the logarithm base 2
* n Number of characters to choose from
* l: Length of the password

In python it can be computed via
```py
math.log2(char_set_length**length)
```


## Human Predictability

Even if we beat the strong password checks, it is likely a naive algorithm would try to guess human patterns.
A ten character password with this character set (including special characters of `!&+=`) could have 1.5683369e+18 combinations to try.
Suppose we have a super computer, can do 100 million trials a per second, this would take approximately 500 years.
What if we could guess it though?
For example, if you have to have a special character, uppercase letter and number then a good guess would be for a minimum of ten char length password.

* First letter being upper case (start of a word)
* Next 5 letters being lowercase (a word)
* The last 4 characters being a number of special character.

So the combinations are 
26 ** 6 * 14**4 = 1.1867308e+13 which would take approximately 1.37 days to crack.


## Conclusion
* Large char set
* Long password
* Random patterns
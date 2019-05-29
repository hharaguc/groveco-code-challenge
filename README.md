# groveco-code-challenge
This is my solution to the [groveco/code-challenge](https://github.com/groveco/code-challenge) problem.

# The Solution
My solution works as follows:
1. Parses and validates the command line arguments with the help of `docopt`
2. Reads the given `store-locations.csv` file
3. Geocodes the starting location
4. Calculates the distance from the starting location to each store from `store-locations.csv` using the [Haversine formula](https://stackoverflow.com/questions/41336756/find-the-closest-latitude-and-longitude). Note that this formula calculates an "as-the-crow-flies"/straight line distance, not driving distance.
5. Prints information about the nearest store and its distance away from the starting location. 

# Assumptions/Caveats
- I assumed that the Haversine formula would be acceptable for calculating the distance.
- I am not doing any validation on `--zip` or `--address` command line arguments. Related to this, I am not doing any validation on the response after calling the MapQuest Geocode API either, outside of checking for status code 200. This code would break if the API returned an empty `results` or `locations` array.

# Let's Get Running
Ensure your Python version is >= 3.5.0. You can check your Python version by running the following command in your terminal:
```python --version```

If you need to update your Python, visit [python.org](https://www.python.org/).

Install the program's dependencies.
```pip install requirements.txt```

You will also need to sign up for an account on [MapQuest's Developer site](https://developer.mapquest.com/plan_purchase/steps/business_edition/business_edition_free/register) in order to get a key for their geocoding API. After you register, copy your `Consumer Key` and paste it into `mapquest_api_key.json`









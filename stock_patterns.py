import pandas as pd
import numpy as np

# Rounding Bottom Detection
def detect_rounding_bottom(df, all_time_low_price):
    current_price = df['Close'].iloc[-1]
    # Initialize the new column as dtype object to accommodate mixed types
    df['rounding_bottom'] = np.nan  # or use pd.NA for more recent pandas versions
    df.loc[
        (current_price > 1.2 * all_time_low_price) & (current_price < 1.4 * all_time_low_price), 
        'rounding_bottom'
    ] = 'Rounding Bottom'
    return df

# Head and Shoulders Detection
def detect_head_shoulder(df):
    # Example logic for detecting Head and Shoulders
    mask_head_shoulder = ((df['High'].shift(2) < df['High'].shift(1)) & 
                          (df['High'].shift(1) > df['High']) & 
                          (df['High'].shift(1) > df['High'].shift(-1)) & 
                          (df['High'] < df['High'].shift(-1)))
    
    mask_inv_head_shoulder = ((df['Low'].shift(2) > df['Low'].shift(1)) & 
                               (df['Low'].shift(1) < df['Low']) & 
                               (df['Low'].shift(1) < df['Low'].shift(-1)) & 
                               (df['Low'] > df['Low'].shift(-1)))

    head_shoulder_pattern = np.empty(len(df), dtype=object)
    head_shoulder_pattern[:] = np.nan
    head_shoulder_pattern[mask_head_shoulder] = 'Head and Shoulder'
    head_shoulder_pattern[mask_inv_head_shoulder] = 'Inverse Head and Shoulder'

    df['head_shoulder_pattern'] = head_shoulder_pattern
    return df

# Multiple Tops and Bottoms Detection
def detect_multiple_tops_bottoms(df, window=3):
    roll_window = window
    df['high_roll_max'] = df['High'].rolling(window=roll_window).max()
    df['low_roll_min'] = df['Low'].rolling(window=roll_window).min()
    df['close_roll_max'] = df['Close'].rolling(window=roll_window).max()
    df['close_roll_min'] = df['Close'].rolling(window=roll_window).min()

    mask_top = (df['high_roll_max'] >= df['High'].shift(1)) & (df['close_roll_max'] < df['Close'].shift(1))
    mask_bottom = (df['low_roll_min'] <= df['Low'].shift(1)) & (df['close_roll_min'] > df['Close'].shift(1))

    multiple_top_bottom_pattern = np.empty(len(df), dtype=object)
    multiple_top_bottom_pattern[:] = np.nan
    multiple_top_bottom_pattern[mask_top] = 'Multiple Top'
    multiple_top_bottom_pattern[mask_bottom] = 'Multiple Bottom'

    df['multiple_top_bottom_pattern'] = multiple_top_bottom_pattern
    return df

# Bullish Engulfing Detection
def detect_bullish_engulfing(df):
    df['bullish_engulfing'] = np.where(
        (df['Close'] > df['Open']) &
        (df['Open'].shift(1) > df['Close'].shift(1)) &
        (df['Open'] < df['Close'].shift(1)) &
        (df['Close'] > df['Open'].shift(1)),
        'Bullish Engulfing',
        np.nan
    )
    return df

# Bearish Engulfing Detection
def detect_bearish_engulfing(df):
    df['bearish_engulfing'] = np.where(
        (df['Close'] < df['Open']) &
        (df['Open'].shift(1) < df['Close'].shift(1)) &
        (df['Open'] > df['Close'].shift(1)) &
        (df['Close'] < df['Open'].shift(1)),
        'Bearish Engulfing',
        np.nan
    )
    return df

# Morning Star Detection
def detect_morning_star(df):
    df['morning_star'] = np.where(
        (df['Close'].shift(2) < df['Open'].shift(2)) &
        (df['Close'].shift(1) < df['Open'].shift(1)) &
        (df['Close'] > df['Open']) &
        (df['Close'] > df['Close'].shift(2)),
        'Morning Star',
        np.nan
    )
    return df

# Evening Star Detection
def detect_evening_star(df):
    df['evening_star'] = np.where(
        (df['Close'].shift(2) > df['Open'].shift(2)) &
        (df['Close'].shift(1) > df['Open'].shift(1)) &
        (df['Close'] < df['Open']) &
        (df['Close'] < df['Close'].shift(2)),
        'Evening Star',
        np.nan
    )
    return df

# Rising Wedge Detection
def detect_rising_wedge(df):
    df['rising_wedge'] = np.where(
        (df['High'].rolling(window=3).max() >= df['High'].shift(1)) &
        (df['Low'].rolling(window=3).min() <= df['Low'].shift(1)) &
        (df['High'] > df['High'].shift(1)) &
        (df['Low'] > df['Low'].shift(1)),
        'Rising Wedge',
        np.nan
    )
    return df

# Falling Wedge Detection
def detect_falling_wedge(df):
    df['falling_wedge'] = np.where(
        (df['High'].rolling(window=3).max() <= df['High'].shift(1)) &
        (df['Low'].rolling(window=3).min() >= df['Low'].shift(1)) &
        (df['High'] < df['High'].shift(1)) &
        (df['Low'] < df['Low'].shift(1)),
        'Falling Wedge',
        np.nan
    )
    return df

# Head and Shoulders Detection
def detect_head_and_shoulders(df):
    df['head_and_shoulders'] = np.where(
        (df['High'].shift(2) < df['High'].shift(1)) &
        (df['High'].shift(1) > df['High']) &
        (df['High'].shift(1) > df['High'].shift(-1)) &
        (df['High'] < df['High'].shift(-1)),
        'Head and Shoulders',
        np.nan
    )
    return df

# Inverted Head and Shoulders Detection
def detect_inverted_head_and_shoulders(df):
    df['inverted_head_and_shoulders'] = np.where(
        (df['Low'].shift(2) > df['Low'].shift(1)) &
        (df['Low'].shift(1) < df['Low']) &
        (df['Low'].shift(1) < df['Low'].shift(-1)) &
        (df['Low'] > df['Low'].shift(-1)),
        'Inverted Head and Shoulders',
        np.nan
    )
    return df

# Function to detect multiple patterns
def detect_multiple_patterns(df):
    df = detect_bullish_engulfing(df)
    df = detect_bearish_engulfing(df)
    df = detect_morning_star(df)
    df = detect_evening_star(df)
    df = detect_rising_wedge(df)
    df = detect_falling_wedge(df)
    df = detect_head_and_shoulders(df)
    df = detect_inverted_head_and_shoulders(df)
    
    return df

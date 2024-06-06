Here is a summary of what I found:
The best ways to balance the data are to use class weighting in the LGBM model to give more importance to minority classes. We can use the under-sampling method, which involves reducing the majority class to have, for example, 1000 instances of class 0 and 1000 instances of class 1. There is a method called SMOTE, which produces more occurrences for the minority class, but apparently, there is negative feedback on this method. The goal is to choose a good method to also avoid overfitting.







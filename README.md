# Studying sermons in the Danish national church

This repository contains code and repo in relation the following publication:

Agersnap, A., Kristensen-McLachlan, R.D, Johansen, K.H., Schjødt, U., & Nielbo, K.L. (2020). "*Sermons as Data: Introducing a Corpus of 11955 Danish Sermons*", *Journal of Cultural Analytics*, [LINK TBC]

In this article, we present a new corpus comprising sermons from pastors in the Evangelical Lutheran Church in Denmark.

## Content

All code used in the article can be found in the folder ```src```. All code is written in Python and is modular. Scripts are numbered sequentially, in the order that they should be executed, with each creating transformed data for the next script to use.

The is presented for evaluative purposes only. These scripts would require substantial refactoring in order to be considered production-ready!

## Output

The final output of these scripts can be found in tabular format in the folder called ```òutput```. There are two relevant tables, one for sermons by pastors who are women (*F*) and one by pastors who are men (*M*). Otherwise, both tables have an identical structure:

| Column | Description|
|--------|:-----------|
```word```| A specific verb that has been extracted from the sermons.
```frequency``` | The raw frequency of how often that verb appears in the sermons.
```han``` | The PMI score for this verb in relation to the pronoun *han* (3rd person, masculine, singular, nominative case)
```ham``` | The PMI score for this verb in relation to the pronoun *han* (3rd person, masculine, singular, oblique case)
```hun``` | The PMI score for this verb in relation to the pronoun *han* (3rd person, feminine, singular, nominative case)
```hende``` | The PMI score for this verb in relation to the pronoun *han* (3rd person, feminine, singular, oblique case)

## Data Access

Unfortunately, for reasons of data protective and privacy, we are unable to share either the sermons or the metadata in relation to this corpus.

However, if you are interested in working with the data for a specific research project, you can contact either of the first two listed authors.



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

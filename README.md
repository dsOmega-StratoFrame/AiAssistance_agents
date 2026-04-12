<!-- mtoc-start -->

* [AI Assistance agents](#ai-assistance-agents)
  * [KBN](#kbn)
  * [[Methodology chosen][2]](#methodology-chosen2)
  * [Contributing](#contributing)
    * [Adding New Node](#adding-new-node)
  * [References](#references)

<!-- mtoc-end -->

# AI Assistance agents

Personal agentic systems for day-to-day AI Assistance.

## KBN

Requires `invoke` & `start-llm-container` external task available in
`shared-scripts`.

```bash
make start-llm-container
pixi run kbn
```

## [Methodology chosen][2]

[Data Science Lifecycle Process][1].
See [Branch Types][3] for branching naming model.

If working in data science workflow, a jira ticket can be used instead of issue number when creating Data Science Lifecycle Process branches
(`<ProjectAbbreviation>-#`). Also a `_` is used as delimiter between
branch type + number and description of the branch. For example,
experiment and model branches made while working on RAN-73 will be:
`experiment/RAN-73_classification-EBM`
`model/RAN-73_custom-churn-classification`

## Contributing

See guidelines in [Contributing](./CONTRIBUTING.md). This projects also
has Docker support, see ["Running in Docker"
section in Contributing](./CONTRIBUTING.md#running-in-docker).

### Adding New Node
1. Add choice to the chat
2. Create new chat-node in [`nodes`](./src/nodes/README.md). Here you define a template and other things
   related to human-llm interaction. One of the important parts of the
   communication is a context. Initialize `VectorStoreManager` here similar to
   already established [config values](./src/config/).
3. One of the values used by `VectorStoreManager` is a data source. Use one of
   the existing or create a new one in [`data_sources`](./src/data_sources/README.md)

## References

[1]: <https://github.com/dslp/dslp> 'Data Science Lifecycle Process'
[2]: <https://youtu.be/nx1VQrGfU8A?t=556> 'Data Science Lifecycle Process
Lecture'
[3]: <https://github.com/dslp/dslp/blob/main/branching/branch-types.md> 'Data
Science Lifecycle Branch Types'

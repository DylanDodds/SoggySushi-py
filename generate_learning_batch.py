from data.dataAgent import DataAgent


def main():
    data_agent = DataAgent()
    data_agent.generate_learning_batch({'source': 'reddit'})


if __name__ == "__main__":
    main()
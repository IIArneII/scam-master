from aiokafka import AIOKafkaProducer
from loguru import logger

from scam_master.services.models.transactions import Message, Topic
from config import KafkaConfig


class KafkaService:
    def __init__(self, kafka_config: dict):
        self._config: KafkaConfig = KafkaConfig(kafka_config) 
        self._producer: AIOKafkaProducer = AIOKafkaProducer(bootstrap_servers=self._config.BOOTSTRAP_SERVERS)
    
    async def start(self) -> None:
        logger.info('Kafka start...')
        await self._producer.start()
    
    async def send_message(self, topic: Topic, message: Message) -> None:
        try:
            logger.info(f'Send message in kafka | Topic: {topic} | Message: {message}')
            await self._producer.send('transactions.status.changed', message.model_dump_json(by_alias=True).encode())
        
        except Exception as e:
            logger.error(e)

    async def stop(self) -> None:
        await self._producer.stop()

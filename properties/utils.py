from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get properties from cache
    properties = cache.get('all_properties')
    if not properties:
        # If not cached, query database
        properties = list(Property.objects.all().values('id', 'title', 'description', 'price', 'location', 'created_at'))
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    return properties


logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    # Connect to the default Redis cache
    redis_conn = get_redis_connection("default")
    
    # Get Redis keyspace stats
    info = redis_conn.info('stats')
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    
    # Calculate hit ratio safely
    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0.0
    
    # Log metrics
    logger.info(f"Redis Cache Metrics: Hits={hits}, Misses={misses}, Hit Ratio={hit_ratio:.2f}")
    
    # Return metrics as a dictionary
    return {
        'hits': hits,
        'misses': misses,
        'hit_ratio': hit_ratio
    }

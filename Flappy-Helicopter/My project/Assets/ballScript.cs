using UnityEngine;

public class BallMovement : MonoBehaviour
{
    public float speed = 5f; // Ball speed
    private Vector2 direction;

    void Start()
    {
        // Start the ball movement in a random direction
        direction = new Vector2(Random.Range(-1f, 1f), Random.Range(-0.5f, 0.5f)).normalized;
    }

    void Update()
    {
        // Move the ball
        transform.position += (Vector3)(direction * speed * Time.deltaTime);
    }

    void OnCollisionEnter2D(Collision2D collision)
    {
        // Reflect the ball when it hits a wall or paddle
        if (collision.gameObject.CompareTag("Wall"))
        {
            Debug.Log("Colliwd with Wall");
            direction.y = -direction.y; // Reverse vertical direction
        }
        else if (collision.gameObject.CompareTag("Paddle"))
        {
            Debug.Log("Colliwd with Paddle");
            direction.x = -direction.x; // Reverse horizontal direction
        }
    }
}


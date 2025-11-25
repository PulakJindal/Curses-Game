using UnityEngine;

public class PlayerScipt : MonoBehaviour
{
    public float moveSpeed;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        float moveX = 0f;
        float moveY = 0f;

        if (Input.GetKey(KeyCode.W) && transform.position.y < 3.8) moveY = 1f;
        if (Input.GetKey(KeyCode.S) && transform.position.y > -3.8) moveY = -1f;

        // Create movement direction and normalize for diagonal movement
        Vector3 moveDirection = new Vector3(moveX, moveY, 0).normalized;

        // Move the object
        transform.position += moveDirection * moveSpeed * Time.deltaTime;
    }
}
